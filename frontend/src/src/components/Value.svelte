<script>
  export let value;

  let name;
  let formattedValue;

  $: {
    name = value[0];
    if (Array.isArray(value[1])) {
      formattedValue = value[1].map(String).join(' ');
    } else {
      formattedValue = String(value[1]);
    }
  }
</script>


<dt><strong>{name}</strong></dt>
<dd>{formattedValue}</dd>
