/*in this page we navigate between three subpages:
 Add to enventory ,Manage enventory, take from enventory*/

import Form from '../components/Addf.tsx';
import InventoryManager from '../components/Navigate.tsx';
import { useState } from 'react';
import TableDemo from '@/components/Table3.tsx';
import Table2 from '@/components/Table2.tsx';

function StockManager() {
  const [cardAction, setCardAction] = useState({
    Add: false,
    Remove: false,
    Manage: false,
  });

  // Callback to receive values from CarouselSpacing
  const handleCardAction = (Add: any, Remove: any, Manage: any) => {
    setCardAction({ Add, Remove, Manage });
  };
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <div className="w-[50%] mt-30 flex flex-col items-center justify-center">
        <div className="w-full m-10 flex justify-center">
          <InventoryManager onCardClick={handleCardAction} />
        </div>
        <div className="flex justify-center items-center">
          {cardAction.Add ? (
            <Form />
          ) : cardAction.Remove ? (
            <TableDemo />
          ) : (
            <Table2 />
          )}
        </div>
      </div>
    </div>
  );
}
export default StockManager;
