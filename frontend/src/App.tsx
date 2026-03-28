import { Route, Routes } from 'react-router-dom'
import AppraisalPage from './pages/AppraisalPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<AppraisalPage />} />
    </Routes>
  )
}

export default App
