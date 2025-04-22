'use client';

import { Checkbox } from '@/components/ui/checkbox';
import { useState } from 'react';
import { Edit, Trash2 } from 'lucide-react';
import { Button } from './ui/button';

const invoices = [
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

export function ManageTable() {
  const [selectedInvoices, setSelectedInvoices] = useState<string[]>([]);

  const toggleInvoice = (invoice: string, checked: boolean) => {
    setSelectedInvoices((prev) =>
      checked ? [...prev, invoice] : prev.filter((i) => i !== invoice),
    );
  };

  return (
    <div className="rounded-md bg-[#10111D] text-[#BFBFBF] font-bold p-1">
      <div className="w-full">
        <div className="grid grid-cols-[0.5fr_1fr_1fr_1fr_1fr_1fr] h-[50px] ">
          <div className="flex items-center justify-center"></div>
          <div className="flex items-center font-medium">
            <button
              type="button"
              // a function to display the menue to filter
              className="text-gray-400 hover:text-gray-200 flex items-center gap-2"
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
              <span>Invoice</span>
            </button>
          </div>
          <div className="flex items-center font-medium">
            <button
              type="button"
              // a function to display the menue to filter
              className="text-gray-400 hover:text-gray-200 flex items-center gap-2"
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
              <span>Status</span>
            </button>
          </div>

          <div className="flex items-center font-medium">
            <button
              type="button"
              // a function to display the menue to filter
              className="text-gray-400 hover:text-gray-200 flex items-center gap-2"
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
              <span>Method</span>
            </button>
          </div>
          <div className="flex items-center justify-center font-medium ">
            <button
              type="button"
              // a function to display the menue to filter
              className="text-gray-400 hover:text-gray-200 flex items-center gap-2"
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
              <span>Amount</span>
            </button>
          </div>

          <div className="flex items-center justify-center font-medium  -translate-x-3">
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
          {invoices.map((invoice) => (
            <div
              key={invoice.invoice}
              className="grid grid-cols-[0.5fr_1fr_1fr_1fr_1fr_1fr] h-[65px] border-b border-gray-800 "
            >
              <div className="flex items-center justify-center">
                <Checkbox
                  checked={selectedInvoices.includes(invoice.invoice)}
                  // handle check behavipur
                />
              </div>
              <div className="flex items-center">{invoice.invoice}</div>
              <div className="flex items-center">{invoice.paymentStatus}</div>
              <div className="flex items-center">{invoice.paymentMethod}</div>
              <div className="flex items-center justify-center w-30 m-4">
                {invoice.totalAmount}
              </div>
              <div className="flex items-center justify-center p-4 ">
                <div className="flex space-x-2">
                  <Button variant="ghost" size="icon">
                    <Edit className="h-4 w-4" />

                    <span className="sr-only">Edit</span>
                  </Button>
                  <Button variant="ghost" size="icon">
                    <Trash2 className="h-4 w-4" />
                    <span className="sr-only">Delete</span>
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ManageTable;
