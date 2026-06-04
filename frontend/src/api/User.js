import api from "@/api/axios.js";

class User{
  getAllUsers(){
    return api.get('users/')
  }

  createUser(data){
    return api.post('users/', data)
  }

  deleteUser(){
    return api.delete(`users/`)
  }

  updateUser(data){
    return api.patch('users/', data)
  }
}

export default new User()
