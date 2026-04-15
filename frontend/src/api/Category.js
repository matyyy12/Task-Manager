import api from "@/api/axios.js";

class Category{
  getAllCategories(){
    return api.get('categories/')
  }
}

export default new Category()
