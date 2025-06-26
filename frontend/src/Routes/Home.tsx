import NavBar from '../components/nav-bar';
import Content from '../components/content';
import { useNavigate } from 'react-router-dom';
import { getToken } from '../token';


function Home() {
  const navigate = useNavigate()

  const token = getToken()
  if (token){
    console.log(token);
  }
  else{
    navigate("/login");
  }


  return (
      <div className='page'>
        <NavBar/>
        <Content/>
      </div>
  )
}

export default Home
