// SearchBar.tsx (Child component)
import { Input } from '@/components/ui/input';
import { Search } from 'lucide-react';

interface SearchBarProps {
  onSearch: (searchTerm: string) => void;
}

function SearchBar({ onSearch }: SearchBarProps) {
  return (
    <div className="relative p-2 w-[90%] md:w-[70%] lg:w-[50%]">
      <div className="absolute right-3 top-3 p-1">
        <Search color="#ffffff" size={20} />
      </div>
      <Input
        type="search"
        placeholder="Search invoices..."
        className="pl-3 pr-8 bg-[#1D2330] border border-[#303846] rounded-md text-white focus:outline-none focus:border-[#505866]"
        onChange={(e) => onSearch(e.target.value)}
      />
    </div>
  );
}

export default SearchBar;
