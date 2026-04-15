import api from "@/api/axios.js";

class Task{
  getAllTasks(){
    return api.get('tasks/')
  }

  createTask(data){
    return api.post('tasks/', data)
  }
}

export default new Task()
