import LogsTable from '../components/Logs.tsx';
import SearchBar from '../components/SearchBar.tsx';

function Logs() {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (term: string) => {
    setSearchTerm(term);
    console.log('Search Term in Logs:', term);
  };
  return (
    <div className="grid gap-0 justify-items-center">
      <div className="grid gap-0 justify-items-center w-[50%]">
        <SearchBar onSearch={handleSearch} />
      </div>

      <LogsTable searchTerm={searchTerm} />
    </div>
  );
}

import { useState } from 'react';

export default Logs;
