import NavBar from '../components/nav-bar';
import Content from '../components/content';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getToken } from '../token';


function Home() {
  const [ loggedIn, setLoggedIn ] = useState<boolean>(false);
  const navigate = useNavigate()
  
  useEffect(()=> {
    const token = getToken()
    console.log(token);
    
    if (token !== "noToken"){
      setLoggedIn(true);
      console.log(token);
      return;
    }
    console.log("navigating");
    
    navigate("/login");

  }, [])



  return loggedIn && (
      <div className='page'>
        <NavBar/>
        <Content/>
      </div>
  )
}

export default Home
