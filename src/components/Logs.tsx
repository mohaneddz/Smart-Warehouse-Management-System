'use client';

import { useState, useEffect, useMemo } from 'react';

// Define the specific types for category and operation
type Category = 'Materials' | 'Food' | 'Chemicals' | 'Electronics' | 'Medicine' | 'Household';
type Operation = 'Insertion' | 'Retrieval';

interface LogEntry {
  item: string;
  category: Category; // Use the defined Category type
  operation: Operation; // Use the defined Operation type
  quantity: number; // Max: 20, Min: 1
  started: string; // Format: YYYY-MM-DD HH:MM:SS
  ended: string;   // Format: YYYY-MM-DD HH:MM:SS
}

interface LogsTableProps {
  searchTerm: string;
}

// Updated logsData array with new categories, operations, and quantities (1-20)
const logsData: LogEntry[] = [
  {
    item: 'Screw Set',
    category: 'Materials',
    operation: 'Insertion',
    quantity: 15,
    started: '2025-04-01 08:30:00',
    ended: '2025-04-01 10:45:00',
  },
  {
    item: 'Canned Beans',
    category: 'Food',
    operation: 'Retrieval',
    quantity: 5,
    started: '2025-04-02 22:00:00',
    ended: '2025-04-03 01:15:00',
  },
  {
    item: 'Cleaning Solution',
    category: 'Chemicals',
    operation: 'Insertion',
    quantity: 10,
    started: '2025-04-03 09:00:00',
    ended: '2025-04-03 12:30:00',
  },
  {
    item: 'USB Cable',
    category: 'Electronics',
    operation: 'Retrieval',
    quantity: 8,
    started: '2025-04-04 14:00:00',
    ended: '2025-04-04 15:45:00',
  },
  {
    item: 'Pain Killers',
    category: 'Medicine',
    operation: 'Insertion',
    quantity: 20,
    started: '2025-04-05 10:00:00',
    ended: '2025-04-05 16:30:00',
  },
  {
    item: 'Paper Towels',
    category: 'Household',
    operation: 'Retrieval',
    quantity: 18,
    started: '2025-04-06 08:00:00',
    ended: '2025-04-06 17:00:00',
  },
  {
    item: 'Wire Spool',
    category: 'Materials',
    operation: 'Retrieval',
    quantity: 3,
    started: '2025-04-07 13:00:00',
    ended: '2025-04-07 14:30:00',
  },
  {
    item: 'Bottled Water',
    category: 'Food',
    operation: 'Insertion',
    quantity: 12,
    started: '2025-04-08 05:00:00',
    ended: '2025-04-08 05:30:00',
  },
  {
    item: 'Bleach',
    category: 'Chemicals',
    operation: 'Retrieval',
    quantity: 1,
    started: '2025-04-09 20:00:00',
    ended: '2025-04-10 04:00:00',
  },
  {
    item: 'Keyboard',
    category: 'Electronics',
    operation: 'Insertion',
    quantity: 6,
    started: '2025-04-10 09:00:00',
    ended: '2025-04-10 17:00:00',
  },
  {
    item: 'Bandages',
    category: 'Medicine',
    operation: 'Retrieval',
    quantity: 9,
    started: '2025-04-11 11:00:00',
    ended: '2025-04-11 12:00:00',
  },
  {
    item: 'Trash Bags',
    category: 'Household',
    operation: 'Insertion',
    quantity: 14,
    started: '2025-04-12 09:30:00',
    ended: '2025-04-12 10:15:00',
  },
];

function LogsTable({ searchTerm }: LogsTableProps) {
  const [sortConfig, setSortConfig] = useState<{
    key: keyof LogEntry | null;
    direction: 'ascending' | 'descending' | null;
  }>({ key: null, direction: null });
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [operationFilter, setOperationFilter] = useState<string>('all');
  const [quantityFilter, setQuantityFilter] = useState<string>('all');
  const [filteredLogs, setFilteredLogs] = useState<LogEntry[]>(logsData);

  useEffect(() => {
    let newFilteredLogs = logsData.filter((log) =>
      Object.values(log).some((value) =>
        String(value).toLowerCase().includes(searchTerm.toLowerCase()),
      ),
    );

    // Category Filter
    if (categoryFilter !== 'all') {
      newFilteredLogs = newFilteredLogs.filter(
        (log) => log.category === categoryFilter,
      );
    }

    // Operation Filter
    if (operationFilter !== 'all') {
      newFilteredLogs = newFilteredLogs.filter(
        (log) => log.operation === operationFilter,
      );
    }

    // Quantity Filter - Updated to reflect 1-20 range
    if (quantityFilter === '1-5') {
      newFilteredLogs = newFilteredLogs.filter((log) => log.quantity >= 1 && log.quantity <= 5);
    } else if (quantityFilter === '6-10') {
      newFilteredLogs = newFilteredLogs.filter(
        (log) => log.quantity >= 6 && log.quantity <= 10,
      );
    } else if (quantityFilter === '11-20') {
      newFilteredLogs = newFilteredLogs.filter((log) => log.quantity >= 11 && log.quantity <= 20);
    }


    setFilteredLogs(newFilteredLogs);
  }, [categoryFilter, operationFilter, quantityFilter, searchTerm]);

  const requestSort = (key: keyof LogEntry) => {
    let direction: 'ascending' | 'descending' = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortedLogs = useMemo(() => {
    if (!sortConfig.key) {
      return filteredLogs;
    }

    return [...filteredLogs].sort((a, b) => {
      const key = sortConfig.key;
      if (key) {
        if (key === 'quantity') {
          const valueA = a[key];
          const valueB = b[key];
          if (valueA < valueB)
            return sortConfig.direction === 'ascending' ? -1 : 1;
          if (valueA > valueB)
            return sortConfig.direction === 'ascending' ? 1 : -1;
          return 0;
        } else if (key === 'started' || key === 'ended') {
          const dateA = new Date(a[key]).getTime();
          const dateB = new Date(b[key]).getTime();
          if (dateA < dateB)
            return sortConfig.direction === 'ascending' ? -1 : 1;
          if (dateA > dateB)
            return sortConfig.direction === 'ascending' ? 1 : -1;
          return 0;
        } else {
          const valueA = String(a[key]);
          const valueB = String(b[key]);
          if (valueA < valueB)
            return sortConfig.direction === 'ascending' ? -1 : 1;
          if (valueA > valueB)
            return sortConfig.direction === 'ascending' ? 1 : -1;
          return 0;
        }
      }
      return 0;
    });
  }, [filteredLogs, sortConfig]);

  const handleCategoryFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setCategoryFilter(event.target.value);
  };

  const handleOperationFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setOperationFilter(event.target.value);
  };

  const handleQuantityFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setQuantityFilter(event.target.value);
  };

  // Dynamically generate unique categories and operations from the updated data
  const uniqueCategories = [
    'all',
    ...(Array.from(new Set(logsData.map((log) => log.category))) as string[]), // Cast to string[] for mapping
  ];
  const uniqueOperations = [
    'all',
    ...(Array.from(new Set(logsData.map((log) => log.operation))) as string[]), // Cast to string[] for mapping
  ];

  // Function to format dates for display (YYYY-MM-DD)
  const formatDate = (dateString: string) => {
    return dateString.split(' ')[0];
  };

  return (
    <div className="rounded-md bg-[#10111D] text-[#BFBFBF] font-bold p-1 mt-8 w-[90%]">
      <div className="w-full">
        <div className="grid grid-cols-6 h-[50px]">
          <div className="flex items-center justify-center">
            <button
              type="button"
              onClick={() => requestSort('item')}
              className="text-gray-400 hover:text-gray-200 flex items-center"
            >
              <span>Item</span>
            </button>
          </div>
          <div className="flex items-center font-medium justify-start">
            <div className="flex items-center gap-2">
              <span className="hidden xl:inline">Category</span>
              <select
                value={categoryFilter}
                onChange={handleCategoryFilterChange}
                className="bg-[#10111D] text-gray-400 border border-gray-700 rounded-md text-sm focus:outline-none"
              >
                {uniqueCategories.map((category) => (
                  <option key={category} value={category}>
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="flex items-center font-medium justify-start">
            <div className="flex items-center gap-2">
              <span className="hidden xl:inline">Operation</span>
              <select
                value={operationFilter}
                onChange={handleOperationFilterChange}
                className="bg-[#10111D] text-gray-400 border border-gray-700 rounded-md text-sm focus:outline-none"
              >
                {uniqueOperations.map((operation) => (
                  <option key={operation} value={operation}>
                    {operation}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="flex items-center justify-center font-medium">
            <div className="flex items-center gap-2">
              <span className="hidden xl:inline">Quantity</span>
              <select
                value={quantityFilter}
                onChange={handleQuantityFilterChange}
                className="bg-[#10111D] text-gray-400 border border-gray-700 rounded-md text-sm focus:outline-none"
              >
                <option value="all">All</option>
                <option value="1-5">1 - 5</option>
                <option value="6-10">6 - 10</option>
                <option value="11-20">11 - 20</option>
              </select>
            </div>
          </div>
          <div className="flex items-center justify-center font-medium">
            <button
              type="button"
              onClick={() => requestSort('started')}
              className="text-gray-400 hover:text-gray-200 flex items-center"
            >
              <span>Started</span>
            </button>
          </div>
          <div className="flex items-center justify-center font-medium">
            <button
              type="button"
              onClick={() => requestSort('ended')}
              className="text-gray-400 hover:text-gray-200 flex items-center"
            >
              <span>Ended</span>
            </button>
          </div>
        </div>

        {/* Table Content */}
        <img
          src="/assets/svgs/SeparatorTable.svg"
          alt="Chart"
          className="w-full h-10"
        />
        <div className="overflow-y-auto h-[390px] [&::-webkit-scrollbar]:w-2 dark:[&::-webkit-scrollbar-track]:bg-[#10121E] dark:[&::-webkit-scrollbar-thumb]:bg-[#303137] overflow-x-hidden">
          {sortedLogs.map((log) => (
            <div
              key={`${log.item}-${log.started}`}
              className="grid grid-cols-6 h-[65px] border-b border-gray-800"
            >
              <div className="flex items-center justify-start pl-3">
                {log.item}
              </div>
              <div className="flex items-center">
                {log.category}
              </div>
              <div className="flex items-center">
                {log.operation}
              </div>
              <div className="flex items-center justify-center">
                {log.quantity}
              </div>
              <div
                className="flex items-center justify-center"
                title={log.started}
              >
                {formatDate(log.started)}
              </div>
              <div className="flex items-center justify-center">
                {formatDate(log.ended)}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default LogsTable;