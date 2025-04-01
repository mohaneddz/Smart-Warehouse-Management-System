import { Input } from '@/components/ui/input';
import { Search } from 'lucide-react';

function SearchBar() {
  return (
    <div className="relative p-8  w-[50%]">
      <div className="absolute left-[82%] p-1 ">
        <Search color="#ffffff" />
      </div>
      <Input type="search" placeholder="Search..." className="pl-8" />
    </div>
  );
}
export default SearchBar;
