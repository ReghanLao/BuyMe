import AuctionForm from "./AuctionForm";
import Login from "./Login";
import ItemSearch from "./AuctionSearch";
import ItemBrowse from "./itemBrowse";

function App() {
  return (
    <div>
      <Login></Login>
      <AuctionForm></AuctionForm>
      <ItemSearch></ItemSearch>
      <ItemBrowse></ItemBrowse>
    </div>
  );
}

export default App;
