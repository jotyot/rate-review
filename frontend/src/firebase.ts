// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCZZz8sw8c1cC-pDduDaaapUED3VsV77KE",
  authDomain: "rating-from-reviews.firebaseapp.com",
  projectId: "rating-from-reviews",
  storageBucket: "rating-from-reviews.appspot.com",
  messagingSenderId: "789898011246",
  appId: "1:789898011246:web:9eb6d79064ec5e1311bc7f",
  measurementId: "G-7Q20F6LJVZ",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

export { app };
