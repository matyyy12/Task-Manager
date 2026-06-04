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

  createInvitation(groupId) {
    return api.post(`groups/${groupId}/invitation`)
  }

  joinByInvitation(token) {
    return api.get(`groups/invitation/${token}`)
  }
}

export default new Groups()
