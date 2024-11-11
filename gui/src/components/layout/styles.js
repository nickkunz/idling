import styled from "styled-components";
import { v } from "../../styles/variables";

export const TextContainer = styled.div`
  width: 50%;
`;

export const TextContainerWide = styled.div`
  width: 75%;
  padding: 0px; // Optional: Add padding for better spacing
  box-sizing: border-box; // Ensure padding is included in the width
  max-height: 93vh; // Set the maximum height to the viewport height
  overflow-y: auto; // Make the container scrollable if content overflows

  /* Hide scrollbar for Webkit browsers (Chrome, Safari) */
  &::-webkit-scrollbar {
    display: none;
  }

  /* Hide scrollbar for IE, Edge, and Firefox */
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
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