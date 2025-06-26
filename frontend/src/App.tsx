import Home from './Routes/Home';
import {BrowserRouter, Routes, Route} from "react-router-dom";
import Login from './Routes/Login';
import CreateAccount from './Routes/CreateAccount';
import TwilioTutorial from './Routes/TwilioTutorial';


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
