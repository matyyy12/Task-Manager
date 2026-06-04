import api from "@/api/axios.js";


class Token{
  login(data){
    return api.post('tokens/login', data)
  }
  register(data){
    return api.post('users/register', data)
  }
  logout(){
    return api.post('tokens/logout')
  }
}

export default new Token()
