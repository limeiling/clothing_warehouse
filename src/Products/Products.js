import React, { useState } from 'react';
const products = (props) => {
    return (
        <ul>{props.loaded && props.catergories.map((catergory, index) => {
            return (
                <li className="details" key={index}>
                    <p>Type: {catergory.type}</p>
                    <p>ID: {catergory.id}</p>
                    <p>name: {catergory.name}</p>
                    <p>manufacturer: {catergory.manufacturer}</p>
                    <p>availability: {catergory.availability}</p>
                </li>)

        })}</ul>
    )
};

export default products;
