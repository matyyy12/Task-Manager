import api from "@/api/axios.js";

class User{
  getAllUsers(){
    return api.get('users/')
  }

  createUser(data){
    return api.post('users/', data)
  }

  deleteUser(id){
    return api.delete(`users/${id}`)
  }

  updateUser(data, id){
    return api.patch(`users/${id}`, data)
  }
}

export default new User()
