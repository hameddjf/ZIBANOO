import { useRoutes } from "react-router-dom";
import AllRouters from "./routers/AllRouters";

const App = () => {
  const Routers = useRoutes(AllRouters);
  return <>{Routers}</>;
};

export default App;
