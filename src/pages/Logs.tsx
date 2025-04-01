import TableDemo from '../components/Table1.tsx';
import Navbar from '../components/Navbar.tsx';
import SearchBar from '../components/SearchBar.tsx';

function Logs() {
  return (
    <div className="grid gap-0 justify-items-center">
      <Navbar />
      <div className="w-[50%] mt-30">
        <div className="grid gap-0 justify-items-center">
          <SearchBar />
        </div>

        <TableDemo />
      </div>
    </div>
  );
}
export default Logs;
