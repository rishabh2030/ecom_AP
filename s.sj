import React, { useState } from 'react';
import axios from 'axios';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';

function YourComponent() {
  const [categories, setCategories] = useState([]);
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const fetchCategories = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/products/categories/');
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
    fetchCategories(); // Fetch categories when menu is clicked
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <>
      <button
        id="demo-positioned-button"
        aria-controls="demo-positioned-menu"
        aria-haspopup="true"
        onClick={handleClick}
      >
        Open Menu
      </button>
      <Menu
        id="demo-positioned-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'top',
          horizontal: 'left',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'left',
        }}
      >
        {categories.map((category, index) => (
          <MenuItem key={index} onClick={handleClose}>
            {category.name}
          </MenuItem>
        ))}
        <MenuItem onClick={handleClose}>Profile</MenuItem>
        <MenuItem onClick={handleClose}>My account</MenuItem>
        <MenuItem onClick={handleClose}>Logout</MenuItem>
      </Menu>
    </>
  );
}

export default YourComponent;
