function Total({ orders }) {
  return (
    <div className="total">
      <h1>Total</h1>
      <p>{orders.length}</p>
    </div>
  );
}

export default Total;
