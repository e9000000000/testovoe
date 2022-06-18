function Orders({ orders }) {
  return (
    <table className="orders">
      <thead>
        <tr>
          <th>№</th>
          <th>заказ №</th>
          <th>стоимость,$</th>
          <th>стоимость,₽</th>
          <th>срок поставки</th>
        </tr>
      </thead>
      <tbody>
        { orders ? orders.map((order, i) => (
          <tr className={order.archived ? "archived": ""}>
            <th>{i+1}</th>
            <th>{order.number}</th>
            <th>{order.cost_usd}</th>
            <th>{order.cost_rub}</th>
            <th>{order.delivery_date}</th>
          </tr>
        )) : (
          <h1>no orders</h1>
        )}
      </tbody>
    </table>
  );
}

export default Orders;
