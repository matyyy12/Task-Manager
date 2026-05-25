import api from "@/api/axios.js";

class Groups {
  getAll() {
    return api.get('groups/')
  }

  getDetails(groupId){
    return api.get(`groups/${groupId}`)
  }

  createGroup(data){
    return api.post('groups/', data)
  }
}

export default new Groups()
