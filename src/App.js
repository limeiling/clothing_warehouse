import React, { useState } from 'react';
import './App.css';
import axios from "axios";
import Cockpit from './Cockpit/Cockpit'
import Products from './Products/Products'

const App = () => {
  const [catergories, setCatergory] = useState(null);
  const [status, setStatus] = useState(false);
  const fetchProductData = async (endPointName) => {
    await axios
      .get("/products/" + endPointName)
      .then(res => {
        setCatergory(res.data);
        setStatus(true);
      });
  };
  return (
    <div>
      <Cockpit
        handleClick={() => fetchProductData("jackets")}
        text='Jacket'
      />
      <Cockpit
        handleClick={() => fetchProductData("shirts")}
        text='Shirt'
      />
      <Cockpit
        handleClick={() => fetchProductData("accessories")}
        text='Accessories'
      />
      <Products loaded={status}
        catergories={catergories} />

    </div>
  )
}
export default App;


