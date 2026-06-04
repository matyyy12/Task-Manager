import api from "@/api/axios.js";


class Token{
  login(data){
    return api.post('tokens/login', data)
  }
  register(data){
    return api.post('users/register', data)
  }
}

export default new Token()
