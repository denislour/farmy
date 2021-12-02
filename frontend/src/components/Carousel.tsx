import React from "react";
import { EuiPanel } from "@elastic/eui";
import styled from "styled-components";

const CarouselWrapper = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

const StyledEuiPanel = styled(EuiPanel)`
  max-width: 450px;
  max-height: 450px;
  border-radius: 50%;

  & > img {
    width: 100%;
    border-radius: 50%;
  }
`;

type CarouselComponentProps = React.PropsWithChildren<{
  items: { label: string; content: JSX.Element }[];
  interval?: number;
}>;

export default function Carousel({
  items,
  interval = 2000,
  ...props
}: CarouselComponentProps) {
  const [current, setCurrent] = React.useState(0);

  React.useEffect(() => {
    const next = (current + 1) % items.length;
    const id = setTimeout(() => setCurrent(next), interval);
    return () => clearTimeout(id);
  }, [current, items.length, interval]);

  return (
    <CarouselWrapper {...props}>
      {items.map((item, i) =>
        current === i ? (
          <div key={i}>
            <StyledEuiPanel paddingSize='l'>{item.content}</StyledEuiPanel>
          </div>
        ) : null
      )}
    </CarouselWrapper>
  );
}