import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
	<>
	  <div className='bg-gradient-to-r from-blue-400 via-teal-400 to-blue-600 h-screen flex items-start justify-center'>
		<input type='text' className='bg-red-100 m-10 outline-nonew'/>
	  </div>
	</>
  )
}

export default App
