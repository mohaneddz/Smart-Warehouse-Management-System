import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

const invoices = [
  {
    invoice: 'INV001',
    paymentStatus: 'Paid',
    totalAmount: '$250.00',
    paymentMethod: 'Credit Card',
    date: '2023-01-15',
    customer: 'John Doe',
  },
  {
    invoice: 'INV002',
    paymentStatus: 'Pending',
    totalAmount: '$150.00',
    paymentMethod: 'PayPal',
    date: '2023-01-20',
    customer: 'Jane Smith',
  },
  {
    invoice: 'INV003',
    paymentStatus: 'Unpaid',
    totalAmount: '$350.00',
    paymentMethod: 'Bank Transfer',
    date: '2023-02-01',
    customer: 'Robert Johnson',
  },
  {
    invoice: 'INV004',
    paymentStatus: 'Paid',
    totalAmount: '$450.00',
    paymentMethod: 'Credit Card',
    date: '2023-02-10',
    customer: 'Emily Davis',
  },
  {
    invoice: 'INV005',
    paymentStatus: 'Paid',
    totalAmount: '$550.00',
    paymentMethod: 'PayPal',
    date: '2023-02-15',
    customer: 'Michael Wilson',
  },
  {
    invoice: 'INV006',
    paymentStatus: 'Pending',
    totalAmount: '$200.00',
    paymentMethod: 'Bank Transfer',
    date: '2023-02-20',
    customer: 'Sarah Brown',
  },
  {
    invoice: 'INV007',
    paymentStatus: 'Unpaid',
    totalAmount: '$300.00',
    paymentMethod: 'Credit Card',
    date: '2023-03-01',
    customer: 'David Miller',
  },
  {
    invoice: 'INV008',
    paymentStatus: 'Paid',
    totalAmount: '$400.00',
    paymentMethod: 'PayPal',
    date: '2023-03-05',
    customer: 'Lisa Taylor',
  },
  {
    invoice: 'INV009',
    paymentStatus: 'Pending',
    totalAmount: '$250.00',
    paymentMethod: 'Bank Transfer',
    date: '2023-03-10',
    customer: 'James Anderson',
  },
  {
    invoice: 'INV010',
    paymentStatus: 'Unpaid',
    totalAmount: '$350.00',
    paymentMethod: 'Credit Card',
    date: '2023-03-15',
    customer: 'Patricia Thomas',
  },
  {
    invoice: 'INV011',
    paymentStatus: 'Paid',
    totalAmount: '$450.00',
    paymentMethod: 'PayPal',
    date: '2023-03-20',
    customer: 'Richard Jackson',
  },
  {
    invoice: 'INV012',
    paymentStatus: 'Pending',
    totalAmount: '$200.00',
    paymentMethod: 'Bank Transfer',
    date: '2023-03-25',
    customer: 'Jennifer White',
  },
];

function TableDemo() {
  return (
    <div className="relative border font-[Arsenal] rounded-md dark overflow-y-scroll [&::-webkit-scrollbar]:w-2 dark:[&::-webkit-scrollbar-track]:bg-[#10121E] dark:[&::-webkit-scrollbar-thumb]:bg-[#303137]">
      <div className="max-h-[400px]">
        <Table className=" bg-[#10111D] dark  text-[#BFBFBF]  font-bold">
          <TableHeader className="sticky top-0 opacity-15">
            <TableRow>
              <TableHead className="w-[100px]">Invoice</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Method</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Customer</TableHead>-
              <TableHead className="text-right">Amount</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody className="h-12">
            {invoices.map((invoice) => (
              <TableRow key={invoice.invoice}>
                <TableCell className="font-medium">{invoice.invoice}</TableCell>
                <TableCell>{invoice.paymentStatus}</TableCell>
                <TableCell>{invoice.paymentMethod}</TableCell>
                <TableCell>{invoice.date}</TableCell>
                <TableCell>{invoice.customer}</TableCell>
                <TableCell className="text-right">
                  {invoice.totalAmount}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
export default TableDemo;
