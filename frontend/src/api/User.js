import api from "@/api/axios.js";

class User{
  getAllUsers(){
    return api.get('users/')
  }
}

export default new User()
