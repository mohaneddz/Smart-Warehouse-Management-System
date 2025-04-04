'use client';

import { Checkbox } from '@/components/ui/checkbox';

import { useState } from 'react';

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

export function RmEdTable() {
  const [selectedInvoices, setSelectedInvoices] = useState<string[]>([]);
  const [quantities, setQuantities] = useState<Record<string, number>>(
    Object.fromEntries(invoices.map((inv) => [inv.invoice, 0])),
  );

  const toggleInvoice = (invoice: string, checked: boolean) => {
    setSelectedInvoices((prev) =>
      checked ? [...prev, invoice] : prev.filter((i) => i !== invoice),
    );
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
          src="/assets/svgs/Seperator.svg"
          alt="Chart"
          className="w-[100%] h-10"
        />
        <div className="overflow-y-auto h-[390px] [&::-webkit-scrollbar]:w-2 dark:[&::-webkit-scrollbar-track]:bg-[#10121E] dark:[&::-webkit-scrollbar-thumb]:bg-[#303137] overflow-x-hidden">
          {invoices.map((invoice) => (
            <div
              key={invoice.invoice}
              className="grid grid-cols-[0.5fr_1fr_1fr_1fr_1fr_1fr] h-[65px] border-b border-gray-800"
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
              <div className="flex items-center justify-center">
                {invoice.totalAmount}
              </div>

              <div className="m-4 flex items-center -translate-x-3 justify-between h-8 w-[75%] rounded-[10px] border border-gray-700 bg-gradient-to-r from-[#10121E] via-[#7F8387]/50 to-[#10121E] ">
                <div className="flex items-center justify-between bg-[#10121E] opacity-80 rounded-xl w-full h-full ">
                  <input
                    value={quantities[invoice.invoice]}
                    className="w-full bg-transparent text-center text-gray-400 focus:outline-none "
                    min="0"
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
