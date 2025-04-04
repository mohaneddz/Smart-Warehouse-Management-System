import LogsTable from '../components/Logs.tsx';
import SearchBar from '../components/SearchBar.tsx';

function Logs() {
  return (
    <div className="grid gap-0 justify-items-center">
      <div className="w-[50%] mt-30">
        <div className="grid gap-0 justify-items-center">
          <SearchBar />
        </div>

        <LogsTable />
      </div>
    </div>
  );
}
export default Logs;
