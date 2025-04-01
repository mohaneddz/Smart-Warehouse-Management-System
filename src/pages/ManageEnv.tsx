import TableDemo from '../components/Table2.tsx';
import Navbar from '../components/Navbar.tsx';
import InventoryManager from '../components/Navigate.tsx';

function Logs() {
  return (
    <div className="grid gap-0 justify-items-center">
      <Navbar />
      <div className="w-[50%] mt-30">
        <div className="w-[100%] m-10 -translate-x-8">
          <InventoryManager />
        </div>

        <TableDemo />
      </div>
    </div>
  );
}
export default Logs;
