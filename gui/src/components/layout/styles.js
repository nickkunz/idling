import styled from "styled-components";
import { v } from "../../styles/variables";

export const TextContainer = styled.div`
  width: 50%;
`;

export const HorizontalList = styled.ul`
  display: flex;
  justify-content: flex-start;
  list-style-type: none;
  padding: 0;

  & > li:not(:last-child) {
    margin-right: 32px;
  }
`;

export const StyledLink = styled.a`
  color: #DAA520; /* Dark yellow gold color */
  text-decoration: none;
`;

export const SLayout = styled.div`
    display: flex;
`;

export const SMain = styled.main`
    padding: calc(${v.smSpacing} * 3.2);

    h1 {
        font-size: 26px;
    }
`;
