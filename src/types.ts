/**
 * Interface for an Order object
 */
export interface Order {
  id: number;
  order_id: number;
  klant_naam: string | null;
  klant_email: string | null;
  product_naam: string;
  bestel_datum: string;
  songtekst?: string;
  status?: string;
  voornaam?: string;
  van_naam?: string;
  relatie?: string;
  datum?: string;
  thema?: string;
  toon?: string;
  structuur?: string;
  rijm?: string;
  beschrijving?: string;
  origin_song_id?: number;
  raw_data?: {
    custom_field_inputs?: Array<{ 
      label?: string; 
      input?: string; 
      name?: string; 
      value?: string; 
    }>;
    products?: Array<{ 
      id?: number;
      title?: string; 
      name?: string;
      custom_field_inputs?: Array<{
        id?: number;
        label?: string;
        input?: string;
        product_id?: number;
        public_label?: string;
      }>;
      pivot?: {
        type?: string | null;
        order_id?: number;
        product_id?: number;
        id?: number;
        tax_pct?: number;
        quantity?: number;
        excl?: number;
        incl?: number;
        orig?: number;
        vat_rate_id?: number;
        sale_discount?: number;
        promo_discount?: number | null;
        tier_discount?: number | null;
        label?: string;
      };
    }>;
    address?: {
      full_name?: string;
      firstname?: string;
      lastname?: string;
      note?: string;
    };
    [key: string]: any; // Allow for other fields in raw_data
  };
  // Legacy fields that might still be used in some parts of the code
  custom_field_inputs?: Array<{ 
    label?: string; 
    input?: string; 
    name?: string; 
    value?: string; 
  }>;
  products?: Array<{ 
    id?: number;
    title?: string; 
    name?: string;
    custom_field_inputs?: Array<{
      id?: number;
      label?: string;
      input?: string;
      product_id?: number;
      public_label?: string;
    }>;
    pivot?: {
      type?: string | null;
      order_id?: number;
      product_id?: number;
      id?: number;
      tax_pct?: number;
      quantity?: number;
      excl?: number;
      incl?: number;
      orig?: number;
      vat_rate_id?: number;
      sale_discount?: number;
      promo_discount?: number | null;
      tier_discount?: number | null;
      label?: string;
    };
  }>;
  address?: {
    full_name?: string;
    firstname?: string;
    lastname?: string;
    note?: string;
  };
}

/**
 * Interface for the result of fetching orders
 */
export interface OrdersFetchResult {
  new_orders: number;
  skipped_orders: number;
  orders: Order[];
}
