import React, { useState } from 'react';
import './App.css';
import axios from "axios";
import Categories from './Categories/Categories'

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
  console.log(catergories)

  return (
    <div>
      <Categories
        handleClick={() => fetchProductData("jackets")}
        text='Jacket'
      />
      <Categories
        handleClick={() => fetchProductData("shirts")}
        text='Shirt'
      />
      <Categories
        handleClick={() => fetchProductData("accessories")}
        text='Accessories'
      />
      {catergories === "ResponseEmptyError" ? <p>NO RESPONSE</p> : <ul>
        {status && catergories.map((catergory, index) => {
          return (

            <li className="details" key={index}>
              <p>name: {catergory.name}</p>
              <p>ID:{catergory.id}</p>
              <p>Type:{catergory.type}</p>
              <p>price:{catergory.price}</p>
              <p>color:{catergory.color}</p>

            </li>)

        })}
      </ul>
      }

    </div>
  )
}
export default App;


