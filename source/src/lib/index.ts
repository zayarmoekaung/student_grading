// place files you want to import through the `$lib` alias in this folder.
import { setAuth,clearAuth } from "./stores/auth";
import { login } from "./services/api";

export {
    setAuth,
    clearAuth,
    login
}