import Navbar from '../components/Navbar.tsx';
import InventoryManager from '../components/Navigate.tsx';
import SimpleForm from '../components/Addf.tsx';
function Logs() {
  return (
    <div className="grid sgap-0 justify-items-center">
      <Navbar />
      <div className="w-[50%] mt-30">
        <div className="w-[100%] m-10 -translate-x-8">
          <InventoryManager />
        </div>
        {/* form */}
        <SimpleForm />
      </div>
    </div>
  );
}
export default Logs;
