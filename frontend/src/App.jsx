import { useState } from 'react'
import { FaSearch } from "react-icons/fa";
import './App.css'

function App() {
  const [Image, setImage] = useState({
    searchText: "",
    image: [],
  })

  async function getImage(event) {
    event.preventDefault()
    const url = "http://127.0.0.1:5000/api/search/text=" + Image.searchText
    const res = await fetch(url)
    const data = await res.json()
    setImage(prevImageSearch => ({
      ...prevImageSearch,
      image: data.image
    })
    )
  }

  function handleChange(event) {
    const {name, value} = event.target
    setImage(prevImageSearch => ({
      ...prevImageSearch,
      [name]: value
    })
    )
  }

  return (
    <body>
      <h1 className="title">Image Search</h1>

      <div className="form">
        <textarea
          className="form-search"
          title="Search"
          name="searchText" 
          value={Image.searchText}
          onChange={handleChange}
        />  
        <button 
          className="button-search" 
          onClick={getImage}
        >
          <FaSearch />
        </button>   
      </div>

      {Image.image.length > 0 && (
        <div>
          <div className="image-container">
            {Image.image.map(imgPath => (
              <img 
                className="image"
                src={imgPath} 
              />
            ))}
          </div>
        </div>
      )}
    </body>
  )
}

export default App
