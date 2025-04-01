'use client';

import { Checkbox } from '@/components/ui/checkbox';
import { Button } from '@/components/ui/button';

import { useState } from 'react';

// Let's add more rows to demonstrate scrolling
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

export function TableDemo() {
  const [selectedInvoices, setSelectedInvoices] = useState<string[]>([]);
  const [quantities, setQuantities] = useState<Record<string, number>>(
    Object.fromEntries(invoices.map((inv) => [inv.invoice, 0])),
  );

  const toggleInvoice = (invoice: string) => {
    setSelectedInvoices((prev) =>
      prev.includes(invoice)
        ? prev.filter((i) => i !== invoice)
        : [...prev, invoice],
    );
  };

  const incrementQuantity = (invoice: string) => {
    setQuantities((prev) => ({
      ...prev,
      [invoice]: prev[invoice] + 1,
    }));
  };

  const decrementQuantity = (invoice: string) => {
    setQuantities((prev) => ({
      ...prev,
      [invoice]: Math.max(0, prev[invoice] - 1),
    }));
  };

  return (
    <div className="border rounded-md bg-[#10111D] dark  text-[#BFBFBF]  font-bold">
      <div className="w-full">
        {/* Table Header */}
        <div className="grid grid-cols-6 border-b h-[65px]">
          <div className="flex items-center justify-center p-4"></div>
          <div className="flex items-center font-medium p-4">Invoice</div>
          <div className="flex items-center font-medium p-4">Status</div>
          <div className="flex items-center font-medium p-4">Method</div>
          <div className="flex items-center justify-end font-medium p-4">
            Amount
          </div>
          <div className="flex items-center justify-center font-medium p-4">
            Quantity
          </div>
        </div>

        {/* Table Body - Scrollable */}
        <div className="overflow-y-auto h-[390px]">
          {' '}
          {/* 6 rows * 65px = 390px */}
          {invoices.map((invoice) => (
            <div
              key={invoice.invoice}
              className="grid grid-cols-6 border-b h-[65px]"
            >
              <div className="flex items-center justify-center p-4">
                <Checkbox
                  checked={selectedInvoices.includes(invoice.invoice)}
                  onCheckedChange={() => toggleInvoice(invoice.invoice)}
                />
              </div>
              <div className="flex items-center font-medium p-4">
                {invoice.invoice}
              </div>
              <div className="flex items-center p-4">
                {invoice.paymentStatus}
              </div>
              <div className="flex items-center p-4">
                {invoice.paymentMethod}
              </div>
              <div className="flex items-center justify-end p-4">
                {invoice.totalAmount}
              </div>
              <div className="flex items-center justify-center p-4">
                <div className="flex flex-col items-center">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6"
                    onClick={() => incrementQuantity(invoice.invoice)}
                  ></Button>
                  <div className="flex items-center justify-center w-16 h-8 border rounded-md shadow-sm bg-background">
                    <input
                      type="number"
                      value={quantities[invoice.invoice]}
                      onChange={(e) => {
                        const value = Number.parseInt(e.target.value) || 0;
                        setQuantities((prev) => ({
                          ...prev,
                          [invoice.invoice]: Math.max(0, value),
                        }));
                      }}
                      className="w-10 text-center bg-transparent border-none focus:outline-none focus:ring-0"
                      min="0"
                    />
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6"
                    onClick={() => decrementQuantity(invoice.invoice)}
                  ></Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
export default TableDemo;
