import { Route, Routes } from 'react-router-dom'
import AppraisalPage from './pages/AppraisalPage'
import AdminPage from './pages/AdminPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<AppraisalPage />} />
      <Route path="/admin" element={<AdminPage />} />
    </Routes>
  )
}

export default App
