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
  className?: string;
  up: boolean;
}) => {
  return (
    <div className={"flex bg-[#10121E] w-full h-[5.125rem] rounded-2xl  text-white m-0 " + props.className} >
      <div
        className={"flex justify-center h-full items-center rounded-l-2xl w-24 " + props.mcolor}
      >
        <img className="" src={props.src} />
      </div>

      <div className="grid grid-cols-2 justify-items-center w-full h-full">
        <div className="flex flex-col justify-center content-center ">
          <p className="text-xl text-slate-400 font-black">{props.title}</p>
          <p className="text-2xl ">{props.amount}%</p>
        </div>
        <div className="flex mt-2 justify-center">
          <p className={`self-center font-bold ${!props.up ? "text-bad" : "text-good"} `}>{props.up_down}%</p>
          <ChevronsUp color="#569992" className={!props.up ? "hidden" : " "} />
          <ChevronsDown color="#995657" className={props.up ? "hidden" : " "} />
        </div>
      </div>
    </div>
  );
};

export default Card;
