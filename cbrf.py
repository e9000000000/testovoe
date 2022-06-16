import xml.etree.ElementTree as ET

import aiohttp

import config


Rates = dict[str, float]

async def get_rates() -> Rates:
    """
    return dict with currency codes and rates to RUB received from ЦБРФ  
    internet connection is required
    """

    async with aiohttp.request("GET", config.CBRF_RATES_URL) as response:
        if response.status // 100 != 2:
            raise ConnectionError(f"can't get rates, {response.status=}")
        root = ET.fromstring(await response.text())

    codes = [c.text for c in root.iter("CharCode")]
    rates = [float(r.text.replace(",", ".")) for r in root.iter("Value")]
    result = {c:r for c, r in zip(codes, rates)}
    result["RUB"] = 1.
    return result

async def convert(cur_from: str, cur_to: str, amount: float, rates: Rates | None=None) -> float:
    """
    convert from one currency to another  
    if no `rates` provided `get_rates` will be used

    Example:
        >>> convert("USD", "RUB", 10., {"RUB": 2., "USD": 100.})
        <<< 5000.0
    """

    cur_from = cur_from.upper()
    cur_to = cur_to.upper()
    if rates is None:
        rates = await get_rates()
    if cur_from not in rates:
        raise ValueError(f"can't find {cur_from=} in {rates=}")
    if cur_to not in rates:
        raise ValueError(f"can't find {cur_to=} in {rates=}")

    return amount * rates[cur_from] / rates[cur_to]
