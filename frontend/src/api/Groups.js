import api from "@/api/axios.js";

class Groups {
  getAll() {
    return api.get('groups/')
  }

  getDetails(groupId){
    return api.get(`groups/${groupId}`)
  }
}

export default new Groups()
