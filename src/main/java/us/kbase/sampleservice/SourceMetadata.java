
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: SourceMetadata</p>
 * <pre>
 * Information about a metadata key as it appeared at the data source.
 * The source key and value represents the original state of the metadata before it was
 * tranformed for ingestion by the sample service.
 * key - the metadata key.
 * skey - the key as it appeared at the data source.
 * svalue - the value as it appeared at the data source.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "key",
    "skey",
    "svalue"
})
public class SourceMetadata {

    @JsonProperty("key")
    private java.lang.String key;
    @JsonProperty("skey")
    private java.lang.String skey;
    @JsonProperty("svalue")
    private Map<String, UObject> svalue;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("key")
    public java.lang.String getKey() {
        return key;
    }

    @JsonProperty("key")
    public void setKey(java.lang.String key) {
        this.key = key;
    }

    public SourceMetadata withKey(java.lang.String key) {
        this.key = key;
        return this;
    }

    @JsonProperty("skey")
    public java.lang.String getSkey() {
        return skey;
    }

    @JsonProperty("skey")
    public void setSkey(java.lang.String skey) {
        this.skey = skey;
    }

    public SourceMetadata withSkey(java.lang.String skey) {
        this.skey = skey;
        return this;
    }

    @JsonProperty("svalue")
    public Map<String, UObject> getSvalue() {
        return svalue;
    }

    @JsonProperty("svalue")
    public void setSvalue(Map<String, UObject> svalue) {
        this.svalue = svalue;
    }

    public SourceMetadata withSvalue(Map<String, UObject> svalue) {
        this.svalue = svalue;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((("SourceMetadata"+" [key=")+ key)+", skey=")+ skey)+", svalue=")+ svalue)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
