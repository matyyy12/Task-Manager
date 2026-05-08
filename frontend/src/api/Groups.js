import api from "@/api/axios.js";

class Groups {
  getAll() {
    return api.get('groups/')
  }
}

export default new Groups()
