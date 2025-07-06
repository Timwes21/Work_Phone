import Home from './Routes/Home.tsx';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from './Routes/Login.tsx';
import CreateAccount from './Routes/CreateAccount.tsx';
import TwilioTutorial from './Routes/TwilioTutorial.tsx';


function App() {
  const app = (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home/>}/>
        <Route path='/login' element={<Login/>}/>
        <Route path='/create-account' element={<CreateAccount/>}/>
        <Route path='/twilio-tutorial' element={<TwilioTutorial/>}/>
      </Routes>
    </BrowserRouter>
  )

  return app;
}

export default App
