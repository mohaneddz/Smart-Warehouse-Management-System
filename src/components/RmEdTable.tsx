'use client';

import { Input } from '@/components/ui/input';
import { Search } from 'lucide-react';
import { useState, useEffect, useMemo } from 'react';

interface Invoice {
  invoice: string;
  paymentStatus: string;
  totalAmount: string;
  paymentMethod: string;
}

const invoicesData: Invoice[] = [
  {
    invoice: 'INV001',
    paymentStatus: 'Paid',
    totalAmount: '$250.00',
    paymentMethod: 'Credit Card',
  },
  {
    invoice: 'INV002',
    paymentStatus: 'Pending',
    totalAmount: '$150.00',
    paymentMethod: 'PayPal',
  },
  {
    invoice: 'INV003',
    paymentStatus: 'Unpaid',
    totalAmount: '$350.00',
    paymentMethod: 'Bank Transfer',
  },
  {
    invoice: 'INV004',
    paymentStatus: 'Paid',
    totalAmount: '$450.00',
    paymentMethod: 'Credit Card',
  },
  {
    invoice: 'INV005',
    paymentStatus: 'Paid',
    totalAmount: '$550.00',
    paymentMethod: 'PayPal',
  },
  {
    invoice: 'INV006',
    paymentStatus: 'Pending',
    totalAmount: '$200.00',
    paymentMethod: 'Bank Transfer',
  },
  {
    invoice: 'INV007',
    paymentStatus: 'Unpaid',
    totalAmount: '$300.00',
    paymentMethod: 'Credit Card',
  },
  {
    invoice: 'INV008',
    paymentStatus: 'Paid',
    totalAmount: '$650.00',
    paymentMethod: 'Credit Card',
  },
  {
    invoice: 'INV009',
    paymentStatus: 'Pending',
    totalAmount: '$750.00',
    paymentMethod: 'PayPal',
  },
  {
    invoice: 'INV010',
    paymentStatus: 'Unpaid',
    totalAmount: '$850.00',
    paymentMethod: 'Bank Transfer',
  },
];

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

export function LogsTable() {
  const [sortConfig, setSortConfig] = useState<{
    key: keyof Invoice | null;
    direction: 'ascending' | 'descending' | null;
  }>({ key: null, direction: null });
  const [amountFilter, setAmountFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [methodFilter, setMethodFilter] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [filteredInvoices, setFilteredInvoices] =
    useState<Invoice[]>(invoicesData);

  useEffect(() => {
    let newFilteredInvoices = invoicesData.filter((invoice) =>
      Object.values(invoice).some((value) =>
        value.toLowerCase().includes(searchTerm.toLowerCase()),
      ),
    );

    // Amount Filter
    if (amountFilter === 'under200') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => parseFloat(invoice.totalAmount.replace('$', '')) < 200,
      );
    } else if (amountFilter === '200to500') {
      newFilteredInvoices = newFilteredInvoices.filter((invoice) => {
        const amount = parseFloat(invoice.totalAmount.replace('$', ''));
        return amount >= 200 && amount <= 500;
      });
    } else if (amountFilter === 'over500') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => parseFloat(invoice.totalAmount.replace('$', '')) > 500,
      );
    }

    // Status Filter
    if (statusFilter !== 'all') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => invoice.paymentStatus === statusFilter,
      );
    }

    // Method Filter
    if (methodFilter !== 'all') {
      newFilteredInvoices = newFilteredInvoices.filter(
        (invoice) => invoice.paymentMethod === methodFilter,
      );
    }

    setFilteredInvoices(newFilteredInvoices);
  }, [amountFilter, statusFilter, methodFilter, searchTerm]);

  const requestSort = (key: keyof Invoice) => {
    let direction: 'ascending' | 'descending' = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortedInvoices = useMemo(() => {
    if (!sortConfig.key) {
      return filteredInvoices;
    }

    return [...filteredInvoices].sort((a, b) => {
      const key = sortConfig.key;
      if (key) {
        if (key === 'totalAmount') {
          const amountA = parseFloat(a[key].replace('$', ''));
          const amountB = parseFloat(b[key].replace('$', ''));
          if (amountA < amountB)
            return sortConfig.direction === 'ascending' ? -1 : 1;
          if (amountA > amountB)
            return sortConfig.direction === 'ascending' ? 1 : -1;
          return 0;
        } else {
          if (a[key] < b[key])
            return sortConfig.direction === 'ascending' ? -1 : 1;
          if (a[key] > b[key])
            return sortConfig.direction === 'ascending' ? 1 : -1;
          return 0;
        }
      }
      return 0;
    });
  }, [filteredInvoices, sortConfig]);

  const handleAmountFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setAmountFilter(event.target.value);
  };

  const handleStatusFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setStatusFilter(event.target.value);
  };

  const handleMethodFilterChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
  ) => {
    setMethodFilter(event.target.value);
  };

  const handleSearch = (term: string) => {
    setSearchTerm(term);
  };

  const uniqueStatuses = [
    'all',
    ...Array.from(new Set(invoicesData.map((inv) => inv.paymentStatus))),
  ];
  const uniqueMethods = [
    'all',
    ...Array.from(new Set(invoicesData.map((inv) => inv.paymentMethod))),
  ];

  return (
    <div className="flex flex-col items-center">
      <SearchBar onSearch={handleSearch} />
      <div className="rounded-md bg-[#10111D] text-[#BFBFBF] font-bold p-1 w-[90%] md:w-[70%] lg:w-[50%]">
        <div className="w-full">
          <div className="grid grid-cols-[1fr_1fr_1fr_1fr_1fr_1fr] h-[50px]">
            <div className="flex items-center justify-center">Items</div>
            <div className="flex items-center font-medium justify-start">
              <button
                type="button"
                onClick={() => requestSort('invoice')}
                className="text-gray-400 hover:text-gray-200 flex items-center"
              >
                <span>Invoice</span>
              </button>
            </div>
            <div className="flex items-center font-medium justify-start">
              <div className="flex items-center gap-2">
                <span>Status</span>
                <select
                  value={statusFilter}
                  onChange={handleStatusFilterChange}
                  className="bg-[#10111D] text-gray-400 border border-gray-700 rounded-md text-sm focus:outline-none"
                >
                  {uniqueStatuses.map((status) => (
                    <option key={status} value={status}>
                      {status.charAt(0).toUpperCase() + status.slice(1)}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="flex items-center font-medium justify-start">
              <div className="flex items-center gap-2">
                <span>Method</span>
                <select
                  value={methodFilter}
                  onChange={handleMethodFilterChange}
                  className="bg-[#10111D] text-gray-400 border w-[55%] border-gray-700 rounded-md text-sm focus:outline-none"
                >
                  {uniqueMethods.map((method) => (
                    <option key={method} value={method}>
                      {method}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <div className="flex items-center justify-center font-medium">
              <div className="flex items-center gap-2">
                <span>Amount</span>
                <select
                  value={amountFilter}
                  onChange={handleAmountFilterChange}
                  className="bg-[#10111D] text-gray-400 border border-gray-700 rounded-md text-sm focus:outline-none"
                >
                  <option value="all">All</option>
                  <option value="under200">Under $200</option>
                  <option value="200to500">$200 - $500</option>
                  <option value="over500">Over $500</option>
                </select>
              </div>
            </div>

            <div className="flex items-center justify-center font-medium">
              Amount
            </div>
          </div>

          {/* Table Content */}
          <img
            src="/assets/svgs/SeparatorTable.svg"
            alt="Chart"
            className="w-full h-10"
          />
          <div className="overflow-y-auto h-[390px] [&::-webkit-scrollbar]:w-2 dark:[&::-webkit-scrollbar-track]:bg-[#10121E] dark:[&::-webkit-scrollbar-thumb]:bg-[#303137] overflow-x-hidden">
            {sortedInvoices.map((invoice) => (
              <div
                key={invoice.invoice}
                className="grid grid-cols-[1fr_1fr_1fr_1fr_1fr_1fr] h-[65px] border-b border-gray-800 "
              >
                <div className="flex items-center justify-center">
                  {invoice.paymentMethod}
                </div>
                <div className="flex items-center">{invoice.invoice}</div>
                <div className="flex items-center">{invoice.paymentStatus}</div>
                <div className="flex items-center">{invoice.paymentMethod}</div>
                <div className="flex items-center justify-center w-30 m-4">
                  {invoice.totalAmount}
                </div>
                <div className="flex items-center justify-center p-4 ">
                  {invoice.totalAmount}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default LogsTable;
