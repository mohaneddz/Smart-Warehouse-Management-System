'use client';

import { Checkbox } from '@/components/ui/checkbox';
import React from 'react';
import { useState, useEffect } from 'react';

const invoicesData = [
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

interface Invoice {
  invoice: string;
  paymentStatus: string;
  totalAmount: string;
  paymentMethod: string;
}

export function RmEdTable() {
  const [selectedInvoices, setSelectedInvoices] = useState<string[]>([]);
  const [quantities, setQuantities] = useState<Record<string, number>>(
    Object.fromEntries(invoicesData.map((inv) => [inv.invoice, 0])),
  );
  const [sortConfig, setSortConfig] = useState<{
    key: keyof Invoice | null;
    direction: 'ascending' | 'descending' | null;
  }>({ key: null, direction: null });
  const [amountFilter, setAmountFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [methodFilter, setMethodFilter] = useState<string>('all');
  const [filteredInvoices, setFilteredInvoices] =
    useState<Invoice[]>(invoicesData);

  useEffect(() => {
    let newFilteredInvoices = invoicesData;

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
  }, [amountFilter, statusFilter, methodFilter]);

  const toggleInvoice = (invoice: string, checked: boolean) => {
    setSelectedInvoices((prev) =>
      checked ? [...prev, invoice] : prev.filter((i) => i !== invoice),
    );
  };

  const handleCheckboxChange = (
    invoice: string,
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    toggleInvoice(invoice, event.target.checked);
  };

  const incrementQuantity = (invoice: string) => {
    setQuantities((prev) => ({ ...prev, [invoice]: prev[invoice] + 1 }));
  };

  const decrementQuantity = (invoice: string) => {
    setQuantities((prev) => ({
      ...prev,
      [invoice]: Math.max(0, prev[invoice] - 1),
    }));
  };

  const requestSort = (key: keyof Invoice) => {
    let direction: 'ascending' | 'descending' = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortedInvoices = React.useMemo(() => {
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

  const uniqueStatuses = [
    'all',
    ...Array.from(new Set(invoicesData.map((inv) => inv.paymentStatus))),
  ];
  const uniqueMethods = [
    'all',
    ...Array.from(new Set(invoicesData.map((inv) => inv.paymentMethod))),
  ];

  return (
    <div className="rounded-md bg-[#10111D] text-[#BFBFBF] font-bold p-1">
      <div className="w-full">
        <div className="grid grid-cols-[0.5fr_1.5fr_1.5fr_1.5fr_1fr_1fr] h-[50px] ">
          <div className="flex items-center justify-center"></div>
          <div className="flex items-center font-medium justify-start">
            {' '}
            {/* Align left */}
            <button
              type="button"
              onClick={() => requestSort('invoice')}
              className="text-gray-400 hover:text-gray-200 flex items-center"
            >
              <span>Invoice</span>
            </button>
          </div>
          <div className="flex items-center font-medium justify-start">
            {' '}
            {/* Align left */}
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
            {' '}
            {/* Align left */}
            <div className="flex items-center gap-2">
              <span>Method</span>
              <select
                value={methodFilter}
                onChange={handleMethodFilterChange}
                className="bg-[#10111D] text-gray-400 border border-gray-700 rounded-md text-sm focus:outline-none"
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
            {' '}
            {/* Keep centered */}
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

          <div className="flex items-center justify-center font-medium  -translate-x-3">
            {' '}
            {/* Keep centered */}
            Quantity
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
              className="grid grid-cols-[0.5fr_1.5fr_1.5fr_1.5fr_1fr_1fr] h-[65px] border-b border-gray-800"
            >
              <div className="flex items-center justify-center">
                <Checkbox
                  checked={selectedInvoices.includes(invoice.invoice)}
                  onCheckedChange={(checked) =>
                    handleCheckboxChange(invoice.invoice, {
                      target: { checked },
                    } as React.ChangeEvent<HTMLInputElement>)
                  }
                  id={`invoice-${invoice.invoice}`}
                />
              </div>
              <div className="flex items-center">{invoice.invoice}</div>
              <div className="flex items-center">{invoice.paymentStatus}</div>
              <div className="flex items-center">{invoice.paymentMethod}</div>
              <div className="flex items-center justify-center">
                {invoice.totalAmount}
              </div>

              <div className="m-4 flex items-center -translate-x-3 justify-between h-8 w-[75%] rounded-[10px] border border-gray-700 bg-gradient-to-r from-[#10121E] via-[#7F8387]/50 to-[#10121E] ">
                <div className="flex items-center justify-between bg-[#10121E] opacity-80 rounded-xl w-full h-full ">
                  <input
                    value={quantities[invoice.invoice]}
                    className="w-full bg-transparent text-center text-gray-400 focus:outline-none "
                    min="0"
                    readOnly
                  />
                  <div className="grid grid-rows-2 gap-1 ">
                    <button
                      type="button"
                      onClick={() => decrementQuantity(invoice.invoice)}
                      className="text-gray-400 hover:text-gray-200"
                    >
                      <svg
                        width="16"
                        height="8"
                        viewBox="0 0 16 8"
                        fill="white"
                        xmlns="http://www.w3.org/2000/svg"
                        transform="rotate(180)"
                      >
                        <path d="M8 8L0.205771 0H15.7942L8 8Z" fill="#8B939B" />
                      </svg>
                    </button>

                    <button
                      type="button"
                      onClick={() => incrementQuantity(invoice.invoice)}
                      className="text-gray-400 hover:text-gray-200"
                    >
                      <svg
                        width="16"
                        height="8"
                        viewBox="0 0 16 8"
                        fill="white"
                        xmlns="http://www.w3.org/2000/svg"
                        transform="rotate(180)"
                      >
                        <path d="M8 0L15.7942 8H0.205771L8 0Z" fill="#8B939B" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default RmEdTable;
