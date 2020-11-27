import React from 'react';
import styled from 'styled-components';

const StyledButton = styled.button`
background-color: #4caf50;
border: none;
color: white;
padding: 15px 32px;
text-align: center;
text-decoration: none;
display: inline-block;
font-size: 16px;
margin: 4px 2px;
cursor: pointer;
width: 250 px;
  
  &:hover {
    backgroud-color: lightgreen;
    color: black;
  }
`;
	
const cockpit = (props) => {
    return (
      <StyledButton onClick={props.handleClick}>
        {props.text}
      </StyledButton>
    )
  }

export default cockpit;