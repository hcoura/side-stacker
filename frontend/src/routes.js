import App from "./App";
import Game from "./Game";

import {
    createBrowserRouter,
    RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
    },
    {
        path: "/game",
        element: <Game />
    }
]);

export default router;