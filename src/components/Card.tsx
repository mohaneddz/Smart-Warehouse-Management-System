import {
  ReactElement,
  JSXElementConstructor,
  ReactNode,
  ReactPortal,
} from 'react';
import { ChevronsDown, ChevronsUp } from 'lucide-react';
const Card = (props: {
  src: string | undefined;
  up_down_pic: string | undefined;
  mcolor: string;
  title:
    | string
    | number
    | boolean
    | ReactElement<any, string | JSXElementConstructor<any>>
    | Iterable<ReactNode>
    | ReactPortal
    | null
    | undefined;
  amount:
    | string
    | number
    | boolean
    | ReactElement<any, string | JSXElementConstructor<any>>
    | Iterable<ReactNode>
    | ReactPortal
    | null
    | undefined;
  up_down:
    | string
    | number
    | boolean
    | ReactElement<any, string | JSXElementConstructor<any>>
    | Iterable<ReactNode>
    | ReactPortal
    | null
    | undefined;
}) => {
  return (
    <div className="grid grid-cols-2 bg-[#10121E] w-[18rem] h-[5.125rem] rounded-2xl  text-white m-0">
      <div
        className="flex justify-center h-full items-center rounded-l-2xl w-[66px]"
        style={{ backgroundColor: props.mcolor }}
      >
        <img className="" src={props.src} />
      </div>

      <div className="grid grid-cols-2 justify-items-center w-full h-full">
        <div className="flex flex-col justify-center content-center ">
          <p className="text-[1.125rem]">{props.title}</p>
          <p className="text-[1.6875rem]">{props.amount}</p>
        </div>
        <div className="flex flex-cols justify-center">
          <p className="self-center">{props.up_down}</p>
          <ChevronsUp color="#1acb2f" className="hidden" />
          <ChevronsDown color="#ce1c1c" />
        </div>
      </div>
    </div>
  );
};

export default Card;
