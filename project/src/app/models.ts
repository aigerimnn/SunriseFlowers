export interface Category {
    id: number;
    name: string;
}

export const category = [
    {
        id: 1,
        name: 'Готовые букеты'
    },
    {
        id: 2,
        name: 'Дополнения'
    },
    {
        id: 3,
        name: 'Открытки'
    },
    {
        id: 4,
        name: 'Шары'
    },
    {
        id: 5,
        name: 'Розы'
    },
    {
        id: 6,
        name: 'Пионы'
    },
    {
        id: 7,
        name: 'Тюльпаны'
    },

]

export interface Product {
    id: number;
    name: string;
    price: number;
    description: string;
    image_url: string;
    images: string[];
    reviews: number;
    categoryName: Category["id"];
  }

  export interface CartItem {
    id: number;
    product: Product;
    cart: number;  // Assuming this represents the cart ID
}

//   export const products = [
//     {
//         id: 1,
//         name: 'Букет слезы вебки',
//         price: 20,
//         description: 'sdfgh',
//         image: 'sdfgh',
//         images: ['sdfgh'],
//         rating: 852,
//         categoryNameID: 1
//     },
//   ]